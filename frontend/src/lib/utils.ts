import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const formatPriceToNaira = (price: number) => {
  return price.toLocaleString("en-NG", {
    style: "currency",
    currency: "NGN",
  });
};

// export   const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     const file = e.target.files?.[0];
//     if (file) {
//       setPreview(URL.createObjectURL(file));
//     } else {
//       setPreview(null);
//     }
//   };
