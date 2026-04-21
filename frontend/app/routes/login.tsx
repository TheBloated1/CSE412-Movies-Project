import type { Route } from "./+types/home";

export function loader() {
  return { name: "temp" };
}

export default function Login({ loaderData }: Route.ComponentProps) {
  return (
    <div className="h-screen flex items-center justify-center">
        Ello!
    </div>
  );
}