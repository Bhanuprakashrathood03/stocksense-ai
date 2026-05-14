"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { api } from "@/lib/api"
import { formatCurrency } from "@/lib/utils"
import { Plus } from "lucide-react"
import type { Portfolio } from "@/types"

export default function PortfolioPage() {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([])

  useEffect(() => { api.get<Portfolio[]>("/portfolios").then(setPortfolios).catch(() => {}) }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Portfolios</h1>
          <p className="text-muted-foreground">Manage your investment portfolios</p>
        </div>
        <Button><Plus className="h-4 w-4 mr-2" />New Portfolio</Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {portfolios.map((p) => (
          <Card key={p.id}>
            <CardHeader>
              <CardTitle>{p.name}</CardTitle>
              <p className="text-sm text-muted-foreground capitalize">{p.risk_profile} risk</p>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold mb-2">{formatCurrency(p.total_value)}</div>
              <div className="text-sm text-muted-foreground">Cash: {formatCurrency(p.cash_balance)}</div>
              <div className="mt-4 space-y-2">
                {p.holdings?.slice(0, 5).map((h) => (
                  <div key={h.id} className="flex justify-between text-sm">
                    <span className="font-medium">{h.symbol}</span>
                    <span>{h.quantity} @ {formatCurrency(h.avg_price)}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
