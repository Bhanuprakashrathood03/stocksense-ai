"use client"

import { useAuthStore } from "@/store/auth"
import { useThemeStore } from "@/store/theme"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Moon, Sun, LogOut, Bell } from "lucide-react"
import { useRouter } from "next/navigation"

export function Header() {
  const { user, logout } = useAuthStore()
  const { theme, toggle } = useThemeStore()
  const router = useRouter()

  return (
    <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-6">
      <div className="flex-1" />
      <Button variant="ghost" size="icon" onClick={toggle}>
        {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
      </Button>
      <Button variant="ghost" size="icon">
        <Bell className="h-4 w-4" />
      </Button>
      <Avatar className="h-8 w-8 cursor-pointer">
        <AvatarFallback className="text-xs">{user?.name?.charAt(0) || user?.email?.charAt(0) || "U"}</AvatarFallback>
      </Avatar>
      <Button variant="ghost" size="sm" onClick={() => { logout(); router.push("/login") }}>
        <LogOut className="h-4 w-4 mr-2" />
        Logout
      </Button>
    </header>
  )
}
