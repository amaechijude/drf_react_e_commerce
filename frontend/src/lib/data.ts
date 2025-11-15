import { axiosInstance, handleApiError } from "./axios.config";
import { Product } from "./types";

export const getProductDetails = async (
  id: string
): Promise<Product | undefined> => {
  try {
    const response = await axiosInstance.get(`/api/products/${id}/`);
    return response.data;
  } catch (error) {
    handleApiError(error, "Failed to fetch product details.");
    return undefined;
  }
};

// categories
export const getCategories = async (
  slug: string
): Promise<Product[] | undefined> => {
  try {
    const response = await axiosInstance.get(`/api/categories/${slug}/`);
    return response.data;
  } catch (error) {
    handleApiError(error, "Failed to fetch categories.");
    return undefined;
  }
};
