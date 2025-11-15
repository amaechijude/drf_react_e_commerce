"use client";
import { axiosInstance, handleApiError } from "@/lib/axios.config";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import z from "zod";
import { Input } from "../ui/input";
import Image from "next/image";
import { Button } from "../ui/button";
import Link from "next/link";

const MAX_AVATAR_SIZE = 2 * 1024 * 1024; // 2MB
const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"];

const registerFormSchema = z
  .object({
    email: z.email("Invalid email address"),

    password: z
      .string()
      .min(8, "Password must be at least 8 characters long")
      .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
      .regex(/[a-z]/, "Password must contain at least one lowercase letter")
      .regex(/[0-9]/, "Password must contain at least one number")
      .regex(
        /[^a-zA-Z0-9]/,
        "Password must contain at least one special character"
      ),

    confirm_password: z
      .string()
      .min(8, "Password must be at least 8 characters long"),

    avatar: z.any().optional(),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
  })
  .superRefine((data, ctx) => {
    const files = data.avatar as FileList | undefined;
    if (files && files.length > 0 && files instanceof FileList) {
      const file = files[0];

      if (file.size > MAX_AVATAR_SIZE) {
        ctx.addIssue({
          code: "custom",
          path: ["avatar"],
          message: `Avatar size must be less than ${
            MAX_AVATAR_SIZE / 1024 / 1024
          } MB`,
        });
      }
      if (!ACCEPTED_IMAGE_TYPES.includes(file.type)) {
        ctx.addIssue({
          code: "custom",
          path: ["avatar"],
          message: "Invalid image type",
        });
      }
    }
  });

type RegisterSchema = z.infer<typeof registerFormSchema>;

// component
export function RegisterForm() {
  const [preview, setPreview] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setPreview(URL.createObjectURL(file));
    } else {
      setPreview(null);
    }
  };

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    // watch,
    // setError,
  } = useForm<RegisterSchema>({
    resolver: zodResolver(registerFormSchema),
  });

  const router = useRouter();

  async function onSubmit(data: RegisterSchema) {
    try {
      // get avatar
      const avatar = (data.avatar as FileList)[0];

      // build form data
      const formData = new FormData();
      formData.append("email", data.email);
      formData.append("password", data.password);
      formData.append("confirm_password", data.confirm_password);
      formData.append("avatar", avatar);

      // send request
      await axiosInstance.post("api/users/register", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      toast.success("Registration successful! login", {
        position: "top-right",
      });
      router.push("/auth/login");
    } catch (error) {
      const errorMesssage = handleApiError(error, "Registration failed");
      toast.error(errorMesssage, { position: "top-center" });
    }
  }

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} className="max-w-md mx-auto p-4">
        <h2 className="text-xl font-semibold mb-4">Register</h2>

        <label className="block mb-2">
          <span className="block text-sm">Email</span>
          <Input
            type="email"
            {...register("email")}
            className="w-full border px-3 py-2 rounded"
          />
          {errors.email && (
            <p className="text-sm text-red-600 mt-1">{errors.email.message}</p>
          )}
        </label>

        <label className="block mb-2">
          <span className="block text-sm">Password</span>
          <Input
            type="password"
            {...register("password")}
            className="w-full border px-3 py-2 rounded"
          />
          {errors.password && (
            <p className="text-sm text-red-600 mt-1">
              {errors.password.message}
            </p>
          )}
        </label>

        <label className="block mb-2">
          <span className="block text-sm">Confirm Password</span>
          <Input
            type="password"
            {...register("confirm_password")}
            className="w-full border px-3 py-2 rounded"
          />
          {errors.confirm_password && (
            <p className="text-sm text-red-600 mt-1">
              {errors.confirm_password.message}
            </p>
          )}
        </label>

        <label className="block mb-4">
          <span className="block text-sm">Avatar (JPG/PNG/WEBP, max 2MB)</span>
          <Input
            type="file"
            accept="image/*"
            {...(register("avatar"), handleFileChange)}
          />
          {errors.avatar && (
            <p className="text-sm text-red-600 mt-1">
              {errors.avatar.message as string}
            </p>
          )}
        </label>

        {preview && (
          <div className="mb-4">
            <span className="block text-sm">Preview</span>
            <Image
              src={preview}
              alt="avatar preview"
              className="w-24 h-24 object-cover rounded"
            />
          </div>
        )}

        {/* login */}
        <div className="block mb-2">
          <Link href={"/auth/login"}>Login</Link>
        </div>
        <Button
          type="submit"
          disabled={isSubmitting}
          className="px-4 py-2 rounded bg-blue-600 text-white"
        >
          {isSubmitting ? "Submitting..." : "Register"}
        </Button>
      </form>
    </>
  );
}
