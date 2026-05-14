export interface User {
  id: string; email: string; name?: string; role: string; plan: string; is_active: boolean; created_at: string
}

export interface Portfolio {
  id: string; name: string; risk_profile: string; total_value: number; cash_balance: number; created_at: string; holdings: Holding[]
}

export interface Holding {
  id: string; symbol: string; quantity: number; avg_price: number; current_price?: number
}

export interface StockQuote {
  symbol: string; price: number; change: number; change_pct: number; volume: number; high_52w?: number; low_52w?: number; name?: string; exchange?: string
}

export interface Alert {
  id: string; symbol: string; condition: string; threshold: number; triggered: boolean; active: boolean; created_at: string
}

export interface Subscription {
  id: string; plan: string; status: string; renews_at?: string; created_at: string
}

export interface WatchlistItem {
  id: string; symbol: string; added_at: string
}

export interface ChatMessage {
  role: string; content: string; session_id: string; created_at: string
}
