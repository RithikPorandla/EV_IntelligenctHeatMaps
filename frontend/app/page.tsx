import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-slate-900 text-white">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
          Personal Portfolio Project
        </p>
      </div>

      <div className="text-center my-12">
        <h1 className="text-4xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500">
          MA EV ChargeMap
        </h1>
        <p className="text-xl mb-8 text-slate-300">
          EV Charging Siting Intelligence for Massachusetts
        </p>
        <p className="max-w-2xl mx-auto text-slate-400 mb-8">
          A data-driven tool to identify optimal locations for electric vehicle charging stations, 
          combining traffic data, demographics, and equity metrics.
        </p>
        
        <Link 
          href="/worcester" 
          className="bg-emerald-500 hover:bg-emerald-600 text-white font-bold py-3 px-8 rounded-lg transition-colors"
        >
          Explore Worcester
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl text-left">
        <div className="p-6 border border-slate-700 rounded-lg bg-slate-800/50">
          <h2 className="text-xl font-bold mb-2 text-emerald-400">Data Engineering</h2>
          <p className="text-slate-400">Robust ETL pipelines processing GIS, traffic, and demographic datasets.</p>
        </div>
        <div className="p-6 border border-slate-700 rounded-lg bg-slate-800/50">
          <h2 className="text-xl font-bold mb-2 text-blue-400">Machine Learning</h2>
          <p className="text-slate-400">Predictive modeling for charging demand and site scoring.</p>
        </div>
        <div className="p-6 border border-slate-700 rounded-lg bg-slate-800/50">
          <h2 className="text-xl font-bold mb-2 text-purple-400">Full Stack</h2>
          <p className="text-slate-400">Interactive map interface built with Next.js, FastAPI, and Postgres.</p>
        </div>
      </div>
    </main>
  );
}
