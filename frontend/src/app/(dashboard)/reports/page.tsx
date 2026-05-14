"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { api } from "@/lib/api"
import { FileText, Download } from "lucide-react"

export default function ReportsPage() {
  const [reports, setReports] = useState<any[]>([])

  useEffect(() => { api.get("/ai/reports").then(setReports).catch(() => {}) }, [])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Reports</h1>
          <p className="text-muted-foreground">AI-generated market reports and analysis</p>
        </div>
        <Button>Generate Report</Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {reports.map((r: any) => (
          <Card key={r.id}>
            <CardHeader className="flex flex-row items-start justify-between">
              <div>
                <CardTitle className="text-base">{r.title}</CardTitle>
                <p className="text-xs text-muted-foreground mt-1">{r.type} • {new Date(r.created_at).toLocaleDateString()}</p>
              </div>
              <FileText className="h-5 w-5 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <Button variant="outline" size="sm" className="w-full"><Download className="h-4 w-4 mr-2" />View Report</Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
