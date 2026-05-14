import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: { unoptimized: true },
  output: "standalone",
  experimental: { optimizePackageImports: ["lucide-react", "recharts"] },
};

export default nextConfig;
