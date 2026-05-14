"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { api } from "@/lib/api"
import { Trash2, Plus } from "lucide-react"
import type { WatchlistItem } from "@/types"

export default function WatchlistPage() {
  const [items, setItems] = useState<WatchlistItem[]>([])
  const [symbol, setSymbol] = useState("")

  const load = () => api.get<WatchlistItem[]>("/watchlist").then(setItems).catch(() => {})
  useEffect(() => { load() }, [])

  const add = async () => {
    if (!symbol) return
    await api.post(`/watchlist?symbol=${symbol.toUpperCase()}`)
    setSymbol("")
    load()
  }

  const remove = async (sym: string) => {
    await api.delete(`/watchlist/${sym}`)
    load()
  }

  return (
    <div className="space-y-6">
      <div><h1 className="text-2xl font-bold">Watchlist</h1><p className="text-muted-foreground">Track your favorite stocks</p></div>

      <div className="flex gap-2 max-w-sm">
        <Input placeholder="Symbol (e.g. AAPL)" value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase())} />
        <Button onClick={add}><Plus className="h-4 w-4" /></Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <Card key={item.id}>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>{item.symbol}</CardTitle>
              <Button variant="ghost" size="icon" onClick={() => remove(item.symbol)}><Trash2 className="h-4 w-4" /></Button>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">Added {new Date(item.added_at).toLocaleDateString()}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
