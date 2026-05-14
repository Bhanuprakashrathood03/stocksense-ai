"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { api } from "@/lib/api"
import { Bot, Send, User } from "lucide-react"

interface Message {
  role: string
  content: string
}

export default function AssistantPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [sessionId, setSessionId] = useState<string | null>(null)

  const send = async () => {
    if (!input.trim()) return
    const userMsg: Message = { role: "user", content: input }
    setMessages((prev) => [...prev, userMsg])
    setInput("")

    try {
      const res = await api.post<{ response: string; session_id: string }>("/ai/chat", {
        message: input,
        session_id: sessionId,
      })
      setSessionId(res.session_id)
      setMessages((prev) => [...prev, { role: "assistant", content: res.response }])
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I couldn't process that request." }])
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div><h1 className="text-2xl font-bold">AI Assistant</h1><p className="text-muted-foreground">Ask anything about stocks, markets, or your portfolio</p></div>

      <Card className="flex-1 mt-4 flex flex-col">
        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((m, i) => (
            <div key={i} className={`flex gap-3 ${m.role === "user" ? "justify-end" : ""}`}>
              <div className={`flex gap-3 max-w-[80%] ${m.role === "user" ? "flex-row-reverse" : ""}`}>
                <div className={`h-8 w-8 rounded-full flex items-center justify-center ${m.role === "user" ? "bg-primary" : "bg-muted"}`}>
                  {m.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                </div>
                <div className={`rounded-lg p-3 text-sm ${m.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"}`}>
                  {m.content}
                </div>
              </div>
            </div>
          ))}
        </CardContent>
        <div className="border-t p-4 flex gap-2">
          <Input placeholder="Ask about a stock..." value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && send()} />
          <Button onClick={send}><Send className="h-4 w-4" /></Button>
        </div>
      </Card>
    </div>
  )
}
