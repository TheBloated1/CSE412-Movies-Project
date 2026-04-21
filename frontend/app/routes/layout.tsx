import type { Route } from "./+types/home";
import {Outlet} from "react-router";
import {Link} from "react-router";

export function loader() {
  return { name: "temp" };
}

export default function Layout({ loaderData }: Route.ComponentProps) {
  return (
    <div>
        <div className="fixed top-0 left-0 w-full z-50 bg-gray-800">
            <div className="mx-auto flex h-16 items-center justify-between px-4 text-white">
                <Link to="/" className="hover:bg-gray-700 px-3 py-2 rounded-full">Home</Link>
            </div>
        </div>
        <main className="pt-16">
            <Outlet />
        </main>
    </div>
  );
}
