"use client";

import Link from "next/link";
import { useParams } from "next/navigation";

import CityMapPage from "@/components/CityMapPage";

export default function Page() {
  const params = useParams<{ city: string }>();
  const city = params?.city ?? "worcester";

  return (
    <div className="min-h-screen bg-zinc-50">
      <header className="border-b border-zinc-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <div className="text-xs font-semibold uppercase tracking-wide text-zinc-500">
              Personal portfolio project
            </div>
            <div className="text-lg font-bold tracking-tight text-zinc-900">
              MA EV ChargeMap
            </div>
          </div>
          <div className="flex items-center gap-3">
            <a
              href="http://localhost:8000/docs"
              className="rounded-xl border border-zinc-200 bg-white px-4 py-2 text-sm font-semibold text-zinc-900 hover:bg-zinc-50"
            >
              API Docs
            </a>
            <Link
              href="/"
              className="rounded-xl bg-zinc-900 px-4 py-2 text-sm font-semibold text-white hover:bg-zinc-800"
            >
              Home
            </Link>
          </div>
        </div>
      </header>

      <CityMapPage citySlug={city} />
    </div>
  );
}
