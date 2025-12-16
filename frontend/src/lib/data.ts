import { axiosInstance } from "./axios.config";
import { Cart, Product } from "./types";

export async function GetProductDetails(
  id: string
): Promise<Product | undefined> {
  try {
    const response = await axiosInstance.get(`/api/products/details/${id}`);
    return response.data;
  } catch (err) {
    console.error(err);
    return undefined;
  }
}

export async function GetAllProductDetails(): Promise<Product[] | undefined> {
  try {
    const response = await axiosInstance.get("/api/products/all");
    return response.data;
  } catch (err) {
    console.error(err);
    return undefined;
  }
}

export async function getUserCart() : Promise<Cart | undefined> {
  try {
    const response = await axiosInstance.get("api/carts");
    console.log(response)
    // if (response.data)
    return response.data
  }
  catch(error) {
    console.log(error)
    return undefined;
  }
}