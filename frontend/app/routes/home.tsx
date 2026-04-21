import type { Route } from "./+types/home";
import {Link} from "react-router-dom";

export function loader() {
  return { name: "temp" };
}

export default function Home({ loaderData }: Route.ComponentProps) {
  return (
    <div className="text-center p-4">
      <h1 className="text-2xl">Welcome to the Movie Catalog!</h1>
      <Link to="/login" className="hover:bg-gray-700 px-3 py-2 rounded-full">Login</Link>
    </div>
  );
}
