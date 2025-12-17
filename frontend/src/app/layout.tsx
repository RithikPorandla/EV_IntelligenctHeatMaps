import type { Metadata } from "next";
import "./globals.css";
// import 'leaflet/dist/leaflet.css'; // Sometimes easier to import in globals or here

export const metadata: Metadata = {
  title: "MA EV ChargeMap",
  description: "EV Charging Siting Intelligence for Massachusetts",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
          {/* Leaflet CSS from CDN as backup if package import is tricky in Next.js SSR */}
          <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
     integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
     crossOrigin=""/>
      </head>
      <body className="h-screen w-screen overflow-hidden flex flex-col">{children}</body>
    </html>
  );
}
