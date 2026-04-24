import { useState } from "react";
import type { Route } from "./+types/home";
import axios from "axios";


export default function Login({ loaderData }: Route.ComponentProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  //Function to handle sending form data to the backend
  async function handleLogin(){
    setLoading(true);
    setError(null);
    try{
      const res = await axios.post("http://127.0.0.1:5000/login", {
        username,
        password,
      });
      const {token, user} = res.data;
      localStorage.setItem("token", token)
      console.log("Successful Login")

    }catch(err){
      console.log("Error: ", err)
      setError("Error on login")
    } finally {
      setLoading(false)
    }
  }
  function handleUsername(e : React.ChangeEvent<HTMLInputElement>){
    setUsername(e.target.value);
  }

    function handlePassword(e : React.ChangeEvent<HTMLInputElement>){
    setPassword(e.target.value);
  }
  return (
    <div className="bg-gray-500 h-screen flex items-center justify-center">
        <div className="bg-gray-200 p-6 flex flex-col gap-3 w-80">
            <input 
            type="text" 
            placeholder="Enter your username" 
            className="pl-2"
            onChange={handleUsername}></input>
            <input 
            type="password" 
            placeholder="Enter your password" 
            className="pl-2"
            onChange={handlePassword}></input>
            <button
             className="hover:bg-gray-700 px-3 py-2 rounded-full"
             onClick={handleLogin}
            >
              Login
            </button>
            <button 
            className="hover:bg-gray-700 px-3 py-2 rounded-full"
            >
              Register Account
            </button>
        </div>
    </div>
  );
}