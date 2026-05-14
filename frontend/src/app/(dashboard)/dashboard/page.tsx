"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { api } from "@/lib/api"
import { formatCurrency, formatPercent, formatNumber } from "@/lib/utils"
import { TrendingUp, TrendingDown, DollarSign, BarChart3, AlertTriangle, Activity } from "lucide-react"

export default function DashboardPage() {
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    api.get("/analytics/overview").then(setData).catch(() => {})
  }, [])

  const stats = [
    { title: "Portfolio Value", value: formatCurrency(data?.total_value || 0), icon: DollarSign, change: "+2.4%" },
    { title: "Cash Balance", value: formatCurrency(data?.total_cash || 0), icon: Activity, change: "0%" },
    { title: "Invested", value: formatCurrency((data?.total_value || 0) - (data?.total_cash || 0)), icon: BarChart3, change: "+1.2%" },
    { title: "Active Alerts", value: "3", icon: AlertTriangle, change: "-1" },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Portfolio overview and market summary</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map(({ title, value, icon: Icon, change }) => (
          <Card key={title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
              <Icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{value}</div>
              <p className={`text-xs ${change.startsWith("+") ? "text-emerald-500" : change.startsWith("-") ? "text-red-500" : "text-muted-foreground"}`}>
                {change}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Market Overview</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-3">
              {["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"].map((s) => (
                <div key={s} className="flex items-center justify-between py-2 border-b last:border-0">
                  <span className="font-medium">{s}</span>
                  <div className="flex items-center gap-2">
                    <Badge variant={s === "AAPL" ? "success" : s === "MSFT" ? "success" : "secondary"} className="text-xs">
                      {s === "AAPL" ? "+1.2%" : s === "MSFT" ? "+0.8%" : s === "NVDA" ? "-0.3%" : "+0.5%"}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>AI Insights</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { text: "AAPL showing bullish MACD crossover", type: "bullish" },
                { text: "MSFT RSI at 68 - approaching overbought", type: "warning" },
                { text: "NVDA support level at $420", type: "info" },
              ].map(({ text, type }) => (
                <div key={text} className="flex items-start gap-3">
                  <div className={`mt-1 h-2 w-2 rounded-full ${type === "bullish" ? "bg-emerald-500" : type === "warning" ? "bg-amber-500" : "bg-blue-500"}`} />
                  <p className="text-sm">{text}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
