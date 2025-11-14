"use client";
import axiosInstance from "@/lib/axios.config";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { set, z } from "zod";
import { fi } from "zod/locales";

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
export default function RegisterForm() {
  const [loading, setIsLoading] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    watch,
    setError,
  } = useForm<RegisterSchema>({
    resolver: zodResolver(registerFormSchema),
  });

  const router = useRouter();

  async function onSubmit(data: RegisterSchema) {
    try {
      setIsLoading(true);
      // get avatar
      const avatar = (data.avatar as FileList)[0];

      // build form data
      const formData = new FormData();
      formData.append("email", data.email);
      formData.append("password", data.password);
      formData.append("confirm_password", data.confirm_password);
      formData.append("avatar", avatar);

      // send request
      const response = await axiosInstance.post(
        "api/users/register",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      toast.success("Registration successful! login", {
        position: "top-right",
      });
      router.push("/auth/login");
    } catch (error) {
      let errorMesssage;
      if (axios.isAxiosError(error)) {
        errorMesssage = error.response?.data;
      } else {
        errorMesssage = "Registration unsuccessfull";
      }
      toast.error(errorMesssage, { position: "top-center" });
    } finally {
      setIsLoading(false);
    }
  };

  return ();
}
