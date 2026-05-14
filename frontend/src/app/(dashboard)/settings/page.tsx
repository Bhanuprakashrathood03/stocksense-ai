"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useThemeStore } from "@/store/theme"
import { useAuthStore } from "@/store/auth"
import { Shield, Moon, Sun, CreditCard } from "lucide-react"

export default function SettingsPage() {
  const { theme, toggle } = useThemeStore()
  const { user } = useAuthStore()

  return (
    <div className="space-y-6 max-w-2xl">
      <div><h1 className="text-2xl font-bold">Settings</h1><p className="text-muted-foreground">Manage your account preferences</p></div>

      <Card>
        <CardHeader><CardTitle>Profile</CardTitle><CardDescription>Your account information</CardDescription></CardHeader>
        <CardContent className="space-y-2">
          <div className="flex justify-between text-sm"><span className="text-muted-foreground">Email</span><span>{user?.email}</span></div>
          <div className="flex justify-between text-sm"><span className="text-muted-foreground">Plan</span><span className="capitalize">{user?.plan}</span></div>
          <div className="flex justify-between text-sm"><span className="text-muted-foreground">Role</span><span className="capitalize">{user?.role}</span></div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle>Appearance</CardTitle><CardDescription>Toggle theme</CardDescription></CardHeader>
        <CardContent>
          <Button variant="outline" onClick={toggle}>
            {theme === "dark" ? <Sun className="h-4 w-4 mr-2" /> : <Moon className="h-4 w-4 mr-2" />}
            {theme === "dark" ? "Light Mode" : "Dark Mode"}
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle>Subscription</CardTitle><CardDescription>Manage your plan</CardDescription></CardHeader>
        <CardContent>
          <div className="flex items-center gap-4">
            <CreditCard className="h-8 w-8 text-muted-foreground" />
            <div>
              <p className="font-medium capitalize">{user?.plan || "Free"} Plan</p>
              <p className="text-sm text-muted-foreground">Upgrade for AI insights and portfolio optimization</p>
            </div>
            <Button className="ml-auto">Upgrade</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
