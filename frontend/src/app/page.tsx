import Link from "next/link"
import { Shield, TrendingUp, Bot, BarChart3, ArrowRight } from "lucide-react"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted">
      <header className="flex items-center justify-between px-6 py-4 max-w-7xl mx-auto">
        <div className="flex items-center gap-2 font-bold text-xl">
          <Shield className="h-6 w-6 text-primary" />
          StockSense AI
        </div>
        <div className="flex gap-4">
          <Link href="/login" className="text-sm font-medium text-muted-foreground hover:text-foreground">Login</Link>
          <Link href="/register" className="text-sm font-medium px-4 py-2 bg-primary text-primary-foreground rounded-md">Get Started</Link>
        </div>
      </header>

      <section className="max-w-7xl mx-auto px-6 pt-24 pb-16 text-center">
        <h1 className="text-5xl font-bold tracking-tight mb-6">AI-Powered Stock Market Intelligence</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
          Institutional-grade analytics, real-time insights, and AI-driven portfolio optimization for individual investors.
        </p>
        <Link href="/register" className="inline-flex items-center gap-2 px-8 py-3 bg-primary text-primary-foreground rounded-md font-medium text-lg hover:bg-primary/90">
          Start Free Trial <ArrowRight className="h-5 w-5" />
        </Link>
      </section>

      <section className="max-w-7xl mx-auto px-6 pb-24 grid md:grid-cols-3 gap-6">
        {[
          { icon: TrendingUp, title: "Real-Time Analytics", desc: "Live market data, technical indicators, and price tracking" },
          { icon: Bot, title: "AI Insights", desc: "LLM-powered analysis, sentiment scoring, and predictive signals" },
          { icon: BarChart3, title: "Portfolio Optimization", desc: "Risk assessment, rebalancing, and performance tracking" },
        ].map(({ icon: Icon, title, desc }) => (
          <div key={title} className="rounded-xl border bg-card p-6 text-left">
            <Icon className="h-10 w-10 text-primary mb-4" />
            <h3 className="font-semibold text-lg mb-2">{title}</h3>
            <p className="text-muted-foreground">{desc}</p>
          </div>
        ))}
      </section>
    </div>
  )
}
