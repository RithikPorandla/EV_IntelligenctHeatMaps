import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-900">
      <main className="mx-auto max-w-5xl px-6 py-16">
        <header className="flex items-center justify-between">
          <div className="flex flex-col">
            <span className="text-sm font-semibold tracking-wide text-zinc-600">
              Personal portfolio project
            </span>
            <h1 className="text-xl font-bold tracking-tight">MA EV ChargeMap</h1>
          </div>
          <Link
            href="/worcester"
            className="rounded-full bg-zinc-900 px-5 py-2.5 text-sm font-semibold text-white shadow hover:bg-zinc-800"
          >
            Explore Worcester
          </Link>
        </header>

        <section className="mt-14 grid gap-10 md:grid-cols-2 md:items-center">
          <div>
            <h2 className="text-4xl font-bold tracking-tight">
              EV charging siting intelligence for Massachusetts
            </h2>
            <p className="mt-4 text-lg leading-8 text-zinc-700">
              This app explores where new EV chargers could have the highest
              impact, balancing demand signals (traffic, activity, density) with
              equity indicators.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Link
                href="/worcester"
                className="inline-flex items-center justify-center rounded-xl bg-zinc-900 px-6 py-3 text-sm font-semibold text-white shadow hover:bg-zinc-800"
              >
                Open the Worcester map
              </Link>
              <a
                href="http://localhost:8000/docs"
                className="inline-flex items-center justify-center rounded-xl border border-zinc-200 bg-white px-6 py-3 text-sm font-semibold text-zinc-900 shadow-sm hover:bg-zinc-50"
              >
                View API schema (FastAPI)
              </a>
            </div>
          </div>

          <div className="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
            <h3 className="text-sm font-semibold text-zinc-600">What this demonstrates</h3>
            <ul className="mt-4 space-y-3 text-sm text-zinc-800">
              <li>
                <span className="font-semibold">Data engineering</span>: ingest → clean → score → serve
              </li>
              <li>
                <span className="font-semibold">Analytics</span>: transparent scoring + top opportunities
              </li>
              <li>
                <span className="font-semibold">ML</span>: a small regression model (v1: synthetic training)
              </li>
              <li>
                <span className="font-semibold">Full-stack</span>: FastAPI + Next.js + interactive maps
              </li>
            </ul>
            <p className="mt-6 text-xs text-zinc-500">
              Note: v1 uses synthetic candidate sites so the app works end-to-end while real GIS
              ingestion is implemented.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}
