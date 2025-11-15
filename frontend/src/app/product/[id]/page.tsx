import { Suspense } from "react";
import { notFound } from "next/navigation";
import { getProductDetails } from "@/lib/data";
import { ProductDetailsSkeleton } from "@/components/product/product-skeleton";
import { ProductDetails } from "@/components/product/product-details";

interface ProductDetailsPageProps {
  params: {
    id: string;
  };
}

export default function ProductDetailsPage({
  params,
}: ProductDetailsPageProps) {
  return (
    <div className="container mx-auto p-4">
      <Suspense fallback={<ProductDetailsSkeleton />}>
        <ProductDetailsContent id={params.id} />
      </Suspense>
    </div>
  );
}

// Separate async component for data fetching
async function ProductDetailsContent({ id }: { id: string }) {
  const product = await getProductDetails(id);

  if (!product) {
    notFound(); // Uses Next.js not-found.tsx
  }

  return <ProductDetails product={product} />;
}
