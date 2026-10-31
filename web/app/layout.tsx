import type { Metadata } from "next";
import { Bricolage_Grotesque, Geist, Geist_Mono, Unbounded } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

// títulos: uma grotesca com personalidade; o corpo segue na Geist
// só o nome "OpenDoor": geométrica e arredondada, combina com o logo
const brand = Unbounded({
  variable: "--font-unbounded",
  subsets: ["latin"],
  weight: ["600"],
});

const display = Bricolage_Grotesque({
  variable: "--font-bricolage",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "OpenDoor",
  description: "Uma Porta Aberta para você contribuir no mundo Open Source.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="pt-BR"
      className={`${geistSans.variable} ${geistMono.variable} ${display.variable} ${brand.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
