"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { api } from "@/lib/api"
import { formatCurrency, formatNumber } from "@/lib/utils"
import { Star, TrendingUp, TrendingDown } from "lucide-react"

export default function StockDetailPage() {
  const { symbol } = useParams<{ symbol: string }>()
  const [quote, setQuote] = useState<any>(null)
  const [insight, setInsight] = useState<any>(null)

  useEffect(() => {
    if (!symbol) return
    api.get(`/stocks/${symbol}`).then(setQuote).catch(() => {})
    api.get(`/ai/insights/${symbol}`).then(setInsight).catch(() => {})
  }, [symbol])

  if (!quote) return <div className="p-6">Loading...</div>

  const isUp = quote.change >= 0

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold">{symbol}</h1>
            <Badge variant="secondary">{quote.name}</Badge>
          </div>
          <p className="text-muted-foreground">{quote.exchange}</p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold">{formatCurrency(quote.price)}</div>
          <div className={`flex items-center gap-1 ${isUp ? "text-emerald-500" : "text-red-500"}`}>
            {isUp ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
            {formatCurrency(quote.change)} ({quote.change_pct?.toFixed(2)}%)
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader><CardTitle className="text-sm">Volume</CardTitle></CardHeader>
          <CardContent><div className="text-xl font-bold">{formatNumber(quote.volume)}</div></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-sm">52W High</CardTitle></CardHeader>
          <CardContent><div className="text-xl font-bold">{quote.high_52w ? formatCurrency(quote.high_52w) : "—"}</div></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-sm">52W Low</CardTitle></CardHeader>
          <CardContent><div className="text-xl font-bold">{quote.low_52w ? formatCurrency(quote.low_52w) : "—"}</div></CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader><CardTitle>AI Analysis</CardTitle></CardHeader>
        <CardContent>
          <p className="text-sm whitespace-pre-wrap">{insight?.analysis || "Loading analysis..."}</p>
        </CardContent>
      </Card>

      <div className="flex gap-2">
        <Button variant="outline"><Star className="h-4 w-4 mr-2" />Watchlist</Button>
        <Button>Set Alert</Button>
      </div>
    </div>
  )
}
