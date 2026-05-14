import { create } from "zustand"
import { api } from "@/lib/api"
import type { User } from "@/types"

interface AuthState {
  user: User | null
  token: string | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, name?: string) => Promise<void>
  logout: () => void
  loadUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: typeof window !== "undefined" ? localStorage.getItem("token") : null,
  loading: false,
  login: async (email, password) => {
    const res = await api.post<{ access_token: string; refresh_token: string }>("/auth/login", { email, password })
    localStorage.setItem("token", res.access_token)
    localStorage.setItem("refresh_token", res.refresh_token)
    set({ token: res.access_token })
    await get().loadUser()
  },
  register: async (email, password, name) => {
    const res = await api.post<{ access_token: string; refresh_token: string }>("/auth/register", { email, password, name })
    localStorage.setItem("token", res.access_token)
    localStorage.setItem("refresh_token", res.refresh_token)
    set({ token: res.access_token })
    await get().loadUser()
  },
  logout: () => {
    localStorage.removeItem("token")
    localStorage.removeItem("refresh_token")
    set({ user: null, token: null })
  },
  loadUser: async () => {
    if (!get().token) return
    set({ loading: true })
    try {
      const user = await api.get<User>("/users/me")
      set({ user, loading: false })
    } catch {
      set({ loading: false })
    }
  },
}))
