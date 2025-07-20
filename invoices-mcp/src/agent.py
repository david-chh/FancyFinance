import argparse
import asyncio
import datetime
from pathlib import Path

from browser_use import Agent, BrowserProfile, BrowserSession, Controller
from browser_use.llm import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Result(BaseModel):
    downloaded_file_path: str


llm = ChatOpenAI(model="gpt-4.1")


async def create_agent(
    *,
    domainOrUrl: str,
    tx_date: datetime.date,
    tx_amount: float,
    tx_reference: str,
    start_browser: bool = True,
):
    # Create a sophisticated task prompt that uses all parameters
    task_prompt = f"""
You are an invoice retrieval specialist tasked with finding and downloading a specific invoice from {domainOrUrl}.

**Target Invoice Details:**
- Transaction Date: {tx_date.strftime("%Y-%m-%d")} (invoice date may be earlier)
- Transaction Amount: ${tx_amount:.2f} (may vary due to currency conversion, taxes, or fees)
- Transaction Reference: {tx_reference}
- Target Website: {domainOrUrl}

**Your Mission:**
Find and download EXACTLY ONE invoice that most closely matches these transaction details. The invoice you're looking for was likely generated between {(tx_date - datetime.timedelta(days=30)).strftime("%Y-%m-%d")} and {tx_date.strftime("%Y-%m-%d")}.

**CRITICAL: Download only ONE file. Once you successfully download a single matching invoice PDF, your task is complete. Do not attempt to download additional files.**

**Search Strategy:**
1. **Website Navigation**: Start by exploring the website structure. Look for:
   - Login/Sign-in areas (you may need to authenticate)
   - Account dashboard or user portal
   - Billing, Invoices, or Payment sections
   - Customer service or support areas
   - Search functionality
   
   **Domain-Specific Navigation:**
   - For fly.io: Navigate directly to fly.io/dashboard/rentr/ for invoice access

2. **Invoice Identification**: When searching through invoices/transactions, look for entries that:
   - Have dates within the expected range (±30 days from {tx_date.strftime("%Y-%m-%d")})
   - Have amounts close to ${tx_amount:.2f} (allow ±20% variance for currency/tax differences)
   - Contain or reference the transaction ID: {tx_reference}
   - Match the general transaction pattern or description
   
3. **Download Process**: Once you locate the correct invoice:
   - **IMPORTANT: Download ONLY ONE PDF file and stop immediately after successful download**
   - The invoice might not be downloaded automatically, so you need to click on the download button
   - Look for download buttons, links, or "View PDF" options
   - Ensure the file is actually downloaded to the downloads folder
   - **STOP EXECUTION once the download is confirmed - do not continue searching or downloading**

**Important Considerations:**
- **Single File Goal**: You must download exactly one invoice file - no more, no less
- **Flexible Matching**: Don't require exact matches - invoice amounts may include taxes, fees, or currency conversions
- **Date Ranges**: Invoice dates are typically before or on the transaction date, but allow some flexibility
- **Best Match Selection**: If you see multiple potential matches, choose the BEST SINGLE match and download only that one
- **Progressive Search**: Start broad (recent invoices) then narrow down using the reference details
- **Error Handling**: If you encounter errors, try alternative paths or methods

**Success Criteria:**
Your task is COMPLETE and SUCCESSFUL when you have downloaded exactly ONE PDF invoice file that reasonably matches the provided transaction details. The downloaded file should be saved to the downloads directory. **IMMEDIATELY STOP after successful download.**

**Failure Scenarios to Handle:**
- If no invoices are found, search more broadly or try different date ranges
- If multiple potential matches exist, select and download ONLY the one with the closest amount and date match
- If the site requires login credentials you don't have, clearly indicate this limitation
- If downloads are restricted, try alternative methods like printing to PDF

**REMEMBER: Your goal is achieved once you download ONE matching invoice PDF file. Do not download multiple files or continue searching after a successful download.**
"""

    initial_actions = [
        {"go_to_url": {"url": f"https://{domainOrUrl}", "new_tab": True}},
    ]

    browser_session = BrowserSession(
        browser_profile=BrowserProfile(
            user_data_dir="~/.config/browseruse/profiles/default-google-chrome",
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            keep_alive=True,
            downloads_path=Path("~/Downloads"),
            # disable_security=True,
        ),
    )

    if start_browser:
        await browser_session.start()

    controller = Controller(
        output_model=Result,
    )

    agent = Agent(
        task=task_prompt,
        llm=llm,
        initial_actions=initial_actions,
        controller=controller,
        use_vision=False,
        browser_session=browser_session,
    )
    return agent


async def main():
    parser = argparse.ArgumentParser(description="Invoice retrieval agent")

    parser.add_argument(
        "--browser-only",
        action="store_true",
        help="Only start the browser session without running the agent",
    )
    args = parser.parse_args()

    if args.browser_only:
        # Just start the browser session and keep it alive
        browser_session = BrowserSession(
            browser_profile=BrowserProfile(
                user_data_dir="~/.config/browseruse/profiles/default-google-chrome",
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                keep_alive=True,
                downloads_path=Path("~/Downloads"),
            )
        )
        await browser_session.start()
        print("Browser session started. Press Ctrl+C to close.")
        try:
            # Keep the browser session alive until user interrupts
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing browser session...")
            await browser_session.close()
        return

    agent = await create_agent(
        domainOrUrl="instagram.com",
        tx_date=datetime.date(2025, 1, 1),
        tx_amount=100,
        tx_reference="1234567890",
    )

    result = await agent.run()
    print(result.model_dump_json())


if __name__ == "__main__":
    asyncio.run(main())
