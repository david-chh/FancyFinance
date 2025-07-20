import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  MessageCircle, 
  BarChart3, 
  FileText, 
  AlertTriangle, 
  Brain, 
  Globe, 
  Zap, 
  CheckCircle, 
  Star,
  Shield,
  Clock,
  TrendingUp,
  Users,
  ArrowRight,
  Play
} from "lucide-react";
import heroImage from "@/assets/hero-cfa.jpg";
import aciLogo from "@/assets/aci-logo.png";
import integrationLogos from "@/assets/integration-logos.png";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-primary to-primary/80 rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-foreground">CFA</span>
          </div>
          <nav className="hidden md:flex space-x-8">
            <a href="#features" className="text-muted-foreground hover:text-foreground transition-colors">Features</a>
            <a href="#integrations" className="text-muted-foreground hover:text-foreground transition-colors">Integrations</a>
            <a href="#how-it-works" className="text-muted-foreground hover:text-foreground transition-colors">How it Works</a>
          </nav>
          <div className="flex items-center space-x-4">
            <Button variant="ghost">Sign In</Button>
            <Button variant="cta">Try CFA Free</Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-b from-muted/30 to-background">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="space-y-4">
                <Badge variant="secondary" className="text-primary">🚀 AI Finance Agent</Badge>
                <h1 className="text-5xl lg:text-6xl font-bold text-foreground leading-tight">
                  The AI Co-Pilot for Your 
                  <span className="text-primary"> Finances</span>
                </h1>
                <p className="text-xl text-muted-foreground leading-relaxed">
                  CFA helps you and your finance team analyze transactions, generate reports, and stay ahead of financial issues — using voice or chat, in seconds.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Button size="lg" variant="cta" className="text-lg px-8 py-4">
                  <Play className="w-5 h-5 mr-2" />
                  Try CFA for Free
                </Button>
                <Button size="lg" variant="outline" className="text-lg px-8 py-4">
                  Book a Demo
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </div>

              {/* Chat Demo Preview */}
              <Card className="p-6 bg-gradient-to-r from-muted/50 to-background border-l-4 border-l-primary">
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center">
                      <MessageCircle className="w-4 h-4 text-muted-foreground" />
                    </div>
                    <div className="bg-secondary rounded-lg p-3 max-w-xs">
                      <p className="text-sm">"How much did we spend on marketing last month?"</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3 justify-end">
                    <div className="bg-primary rounded-lg p-3 max-w-xs text-primary-foreground">
                      <p className="text-sm">We spent €12,450 on marketing in December. Here's the breakdown by channel...</p>
                    </div>
                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                      <Brain className="w-4 h-4 text-primary-foreground" />
                    </div>
                  </div>
                </div>
              </Card>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-accent/20 rounded-2xl blur-3xl transform rotate-6"></div>
              <img 
                src={heroImage} 
                alt="CFA AI Finance Dashboard" 
                className="relative z-10 rounded-2xl shadow-2xl w-full"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4">
              Everything Your Finance Team Needs
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              CFA combines AI intelligence with practical automation to transform how you manage finances.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: MessageCircle,
                title: "Chat & Voice Querying",
                description: "Ask financial questions naturally and get instant, accurate answers with full context."
              },
              {
                icon: BarChart3,
                title: "Live Finance Dashboard",
                description: "Real-time KPIs, alerts, and financial metrics in a customizable dashboard."
              },
              {
                icon: FileText,
                title: "One-click Reporting",
                description: "Generate tax-ready, investor-friendly reports instantly with zero manual work."
              },
              {
                icon: AlertTriangle,
                title: "Anomaly Detection",
                description: "Proactive alerts for unusual transactions and potential financial risks."
              },
              {
                icon: Brain,
                title: "Agent-to-Agent Architecture",
                description: "Explainable decisions with deterministic sub-agents for trust and compliance."
              },
              {
                icon: Globe,
                title: "Website Automation",
                description: "MCP-powered agent logs into websites to download invoices and documents automatically."
              }
            ].map((feature, index) => (
              <Card key={index} className="p-6 hover:shadow-lg transition-shadow duration-300">
                <CardContent className="p-0">
                  <div className="space-y-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                      <feature.icon className="w-6 h-6 text-primary" />
                    </div>
                    <h3 className="text-xl font-semibold text-foreground">{feature.title}</h3>
                    <p className="text-muted-foreground">{feature.description}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4">
              How CFA Works
            </h2>
            <p className="text-xl text-muted-foreground">
              Simple 4-step process to revolutionize your finance operations
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            {[
              {
                step: "01",
                title: "Connect",
                description: "Link your tools and data sources securely"
              },
              {
                step: "02",
                title: "Ask",
                description: "Query finances via chat or voice naturally"
              },
              {
                step: "03",
                title: "Analyze",
                description: "CFA processes with AI agents and RAG"
              },
              {
                step: "04",
                title: "Act",
                description: "Get insights, reports, and automated actions"
              }
            ].map((step, index) => (
              <div key={index} className="text-center space-y-4">
                <div className="w-16 h-16 bg-gradient-to-r from-primary to-accent rounded-full flex items-center justify-center mx-auto">
                  <span className="text-white font-bold text-lg">{step.step}</span>
                </div>
                <h3 className="text-xl font-semibold text-foreground">{step.title}</h3>
                <p className="text-muted-foreground">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Integrations */}
      <section id="integrations" className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4">
              Connected to Everything That Powers Your Business
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              CFA connects to your financial ecosystem — from your bank account to Notion pages — using direct APIs, AI agents, and our MCP partnership.
            </p>
          </div>

          <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6">
            {[
              { name: "Google Sheets", logo: "📊" },
              { name: "Notion", logo: "📝" },
              { name: "SharePoint", logo: "🏢" },
              { name: "Gmail", logo: "📧" },
              { name: "Google Drive", logo: "💾" },
              { name: "Airtable", logo: "🗂️" },
              { name: "Supabase", logo: "⚡" },
              { name: "Agent Mail", logo: "📮" },
              { name: "Stripe", logo: "💳" },
              { name: "CoinMarketCap", logo: "₿" },
              { name: "Holded", logo: "📈" },
              { name: "Paddle", logo: "🚣" }
            ].map((integration, index) => (
              <Card key={index} className="p-4 text-center hover:shadow-md transition-shadow">
                <CardContent className="p-2">
                  <div className="w-12 h-12 bg-primary/10 rounded-lg mx-auto mb-3 flex items-center justify-center text-2xl">
                    {integration.logo}
                  </div>
                  <p className="font-medium text-foreground">{integration.name}</p>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="mt-16 text-center">
            <div className="flex items-center justify-center mb-4">
              <Badge variant="secondary" className="text-accent mr-3">✅ Powered by</Badge>
              <img src={`${aciLogo}?v=${Date.now()}`} alt="ACI.dev" className="h-8 w-auto bg-white rounded px-2 py-1 border border-gray-300" style={{filter: 'contrast(2) brightness(0.3)'}} />
            </div>
            <p className="text-muted-foreground">
              Advanced integrations powered by our strategic partnership with ACI.dev
            </p>
          </div>
        </div>
      </section>

      {/* Strategic Partnerships */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4">
              Built with the Best in AI and Automation
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              CFA is integrated with getivy.io, enabling background automation for document retrieval and embedded workflows.
            </p>
          </div>

          <Card className="p-8 bg-gradient-to-r from-primary/5 to-accent/5 border-primary/20">
            <CardContent className="p-0 text-center">
              <div className="space-y-6">
                <div className="flex justify-center items-center space-x-8">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-4">
                      <Brain className="w-8 h-8 text-primary-foreground" />
                    </div>
                    <p className="font-semibold text-foreground">CFA</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-0.5 bg-gradient-to-r from-primary to-accent"></div>
                    <Zap className="w-6 h-6 text-accent" />
                    <div className="w-8 h-0.5 bg-gradient-to-r from-accent to-primary"></div>
                  </div>
                  <div className="text-center">
                    <img src={`${aciLogo}?v=${Date.now()}`} alt="ACI.dev" className="w-16 h-16 mx-auto mb-4 rounded-full p-3 bg-white shadow-lg border border-gray-300" style={{filter: 'contrast(2) brightness(0.3)'}} />
                    <p className="font-semibold text-foreground">ACI.dev</p>
                  </div>
                </div>
                <p className="text-lg text-muted-foreground">
                  Seamless automation via API and MCP for end-to-end finance tasks
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4">
              Trusted by Finance Teams Across Europe
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                quote: "CFA saved us over 14 hours/month",
                metric: "14 hours",
                company: "SaaS Startup",
                benefit: "Time saved monthly"
              },
              {
                quote: "Spotted €7,200 in missed invoices",
                metric: "€7,200",
                company: "Digital Agency", 
                benefit: "Revenue recovered"
              },
              {
                quote: "Finally a finance tool that works like a teammate",
                metric: "100%",
                company: "eCommerce Business",
                benefit: "Team satisfaction"
              }
            ].map((testimonial, index) => (
              <Card key={index} className="p-6 text-center">
                <CardContent className="p-0 space-y-6">
                  <div className="space-y-2">
                    <div className="text-3xl font-bold text-primary">{testimonial.metric}</div>
                    <p className="text-sm text-muted-foreground">{testimonial.benefit}</p>
                  </div>
                  <div className="space-y-4">
                    <div className="flex justify-center space-x-1">
                      {[...Array(5)].map((_, i) => (
                        <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                      ))}
                    </div>
                    <p className="text-foreground italic">"{testimonial.quote}"</p>
                    <p className="text-sm text-muted-foreground font-medium">{testimonial.company}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Trust & Compliance */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-foreground mb-4">
              Enterprise-Ready Security & Compliance
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Shield,
                title: "GDPR Compliant",
                description: "Full compliance with European data protection regulations"
              },
              {
                icon: CheckCircle,
                title: "Explainable Decisions",
                description: "Every action has a traceable source for full transparency"
              },
              {
                icon: Brain,
                title: "No Hallucination",
                description: "Core logic handled by deterministic sub-agents and rules"
              }
            ].map((item, index) => (
              <Card key={index} className="p-6 text-center">
                <CardContent className="p-0 space-y-4">
                  <div className="w-16 h-16 bg-success/10 rounded-full flex items-center justify-center mx-auto">
                    <item.icon className="w-8 h-8 text-success" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground">{item.title}</h3>
                  <p className="text-muted-foreground">{item.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 bg-gradient-to-r from-primary to-accent">
        <div className="container mx-auto px-4 text-center">
          <div className="max-w-4xl mx-auto space-y-8">
            <h2 className="text-5xl font-bold text-white">
              Let CFA Handle the Numbers – So You Can Focus on Growth
            </h2>
            <p className="text-xl text-white/90">
              Trusted by founders and finance teams to automate, organize, and protect their financial data.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="secondary" className="text-lg px-8 py-4">
                <Play className="w-5 h-5 mr-2" />
                Try CFA for Free
              </Button>
              <Button size="lg" variant="outline" className="text-lg px-8 py-4 border-white/20 text-white hover:bg-white/10 hover:border-white/40">
                Book a Demo
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </div>

            <div className="flex justify-center items-center space-x-8 text-white/80 text-sm pt-8">
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4" />
                <span>Setup in 5 minutes</span>
              </div>
              <div className="flex items-center space-x-2">
                <Users className="w-4 h-4" />
                <span>No training required</span>
              </div>
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4" />
                <span>ROI from day one</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-foreground text-white">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold">CFA</span>
              </div>
              <p className="text-gray-400">
                The AI Co-Pilot for Your Finances
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <div className="space-y-2 text-gray-400">
                <a href="#features" className="block hover:text-white transition-colors">Features</a>
                <a href="#integrations" className="block hover:text-white transition-colors">Integrations</a>
                <a href="#" className="block hover:text-white transition-colors">Pricing</a>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <div className="space-y-2 text-gray-400">
                <a href="#" className="block hover:text-white transition-colors">About</a>
                <a href="#" className="block hover:text-white transition-colors">Careers</a>
                <a href="#" className="block hover:text-white transition-colors">Contact</a>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <div className="space-y-2 text-gray-400">
                <a href="#" className="block hover:text-white transition-colors">Privacy</a>
                <a href="#" className="block hover:text-white transition-colors">Terms</a>
                <a href="#" className="block hover:text-white transition-colors">GDPR</a>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 CFA - Chief Financial Agent. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
