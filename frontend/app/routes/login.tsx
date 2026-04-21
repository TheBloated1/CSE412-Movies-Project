import type { Route } from "./+types/home";

export function loader() {
  return { name: "temp" };
}

export default function Login({ loaderData }: Route.ComponentProps) {
  return (
    <div className="bg-gray-500 h-screen flex items-center justify-center">
        <div className="bg-gray-200 p-6 flex flex-col gap-3 w-80">
            <input type="text" placeholder="Enter your username" className="pl-2"></input>
            <input type="password" placeholder="Enter your password" className="pl-2"></input>
            <button className="hover:bg-gray-700 px-3 py-2 rounded-full">Input</button>
        </div>
    </div>
  );
}