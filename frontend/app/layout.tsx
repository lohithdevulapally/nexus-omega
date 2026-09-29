import type { Metadata } from 'next';
import './globals.css';
import { Sidebar } from '@/components/layout/Sidebar';
import { TopBar } from '@/components/layout/TopBar';

export const metadata: Metadata = {
  title: 'NEXUS-Ω | Enterprise AI Decision Intelligence Cockpit',
  description:
    'Mission control for enterprise memory, causal knowledge, counterfactual simulation, and human-in-the-loop controlled action.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark h-full bg-[#060A12] text-slate-100 antialiased">
      <body className="h-full flex overflow-hidden bg-[#060A12] text-slate-100 selection:bg-cyan-500/20 selection:text-cyan-200">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0 h-screen overflow-y-auto">
          <TopBar />
          <main className="flex-1 p-6 md:p-8 max-w-[1600px] w-full mx-auto space-y-6">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
