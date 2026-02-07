import { useState } from "react";

export default function AuthCard() {
  const [isLogin, setIsLogin] = useState(true);

  // signup state
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // login state
  const [loginIdentifier, setLoginIdentifier] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!isLogin) {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/auth/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            username,
            password,
            confirmPassword,
          }),
        });

        const data = await res.json();

        if (!res.ok) {
          alert(data.detail || "Signup failed");
          return;
        }

        alert("Signup successful. Please login.");
        setIsLogin(true);
      } catch (err) {
        console.error(err);
        alert("Network error");
      }
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 p-4">
      <div className="w-full max-w-md p-8 bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl shadow-xl">
        <h1 className="text-3xl font-semibold text-white mb-2 text-center">
          DreamFrame
        </h1>

        <p className="text-sm text-gray-300 mb-8 text-center">
          {isLogin ? "Login to enter your AI dream world" : "Create a new account"}
        </p>

        <form className="space-y-6" onSubmit={handleSubmit}>
          {!isLogin ? (
            <>
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-white/10 text-white"
              />

              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-white/10 text-white"
              />

              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-white/10 text-white"
              />

              <input
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-white/10 text-white"
              />
            </>
          ) : (
            <>
              <input
                type="text"
                placeholder="Username or Email"
                value={loginIdentifier}
                onChange={(e) => setLoginIdentifier(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-white/10 text-white"
              />

              <input
                type="password"
                placeholder="Password"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-lg bg-white/10 text-white"
              />
            </>
          )}

          <button
            type="submit"
            className="w-full py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold text-white"
          >
            {isLogin ? "Login" : "Sign Up"}
          </button>
        </form>

        <p className="text-sm text-gray-400 mt-6 text-center">
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <button
            type="button"
            onClick={toggleForm}
            className="text-purple-400 font-semibold hover:underline"
          >
            {isLogin ? "Sign Up" : "Login"}
          </button>
        </p>
      </div>
    </div>
  );
}