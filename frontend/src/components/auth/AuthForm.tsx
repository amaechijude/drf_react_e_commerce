import { LoginForm } from "./login-form";
import { RegisterForm } from "./register-form";

interface AuthFormProps {
  variant: "login" | "register";
}

export function AuthForm({ variant }: AuthFormProps) {
  const child = () => {
    switch (variant) {
      case "login":
        return <LoginForm />;
      case "register":
        return <RegisterForm />;
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full p-4 bg-white rounded shadow-md">
        {child()}
      </div>
    </div>
  );
}
