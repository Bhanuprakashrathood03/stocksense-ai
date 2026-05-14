"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { api } from "@/lib/api"
import { Shield, Users } from "lucide-react"

export default function AdminPage() {
  const [users, setUsers] = useState<any[]>([])
  const [stats, setStats] = useState<any>(null)

  useEffect(() => {
    api.get("/admin/users").then(setUsers).catch(() => {})
    api.get("/admin/stats").then(setStats).catch(() => {})
  }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <Shield className="h-6 w-6 text-primary" />
        <h1 className="text-2xl font-bold">Admin Panel</h1>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card><CardHeader><CardTitle className="text-sm">Total Users</CardTitle></CardHeader><CardContent><div className="text-2xl font-bold">{stats?.total_users || 0}</div></CardContent></Card>
        <Card><CardHeader><CardTitle className="text-sm">Active Users</CardTitle></CardHeader><CardContent><div className="text-2xl font-bold">{stats?.active_users || 0}</div></CardContent></Card>
      </div>

      <Card>
        <CardHeader><CardTitle><Users className="h-5 w-5 inline mr-2" />Users</CardTitle></CardHeader>
        <CardContent>
          <div className="space-y-2">
            {users.map((u) => (
              <div key={u.id} className="flex items-center justify-between py-2 border-b last:border-0">
                <div>
                  <p className="font-medium">{u.email}</p>
                  <p className="text-sm text-muted-foreground">{u.name || "—"} • {new Date(u.created_at).toLocaleDateString()}</p>
                </div>
                <div className="flex gap-2">
                  <Badge variant={u.role === "admin" ? "default" : "secondary"}>{u.role}</Badge>
                  <Badge variant={u.plan === "free" ? "outline" : "success"}>{u.plan}</Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
