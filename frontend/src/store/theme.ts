import { create } from "zustand"

type Theme = "light" | "dark"

interface ThemeState {
  theme: Theme
  toggle: () => void
}

export const useThemeStore = create<ThemeState>((set) => ({
  theme: "dark",
  toggle: () => set((s) => ({ theme: s.theme === "dark" ? "light" : "dark" })),
}))
