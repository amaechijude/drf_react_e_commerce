"use client";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { ShippingAddress as AddressType } from "@/lib/types";
import { axiosInstance } from "@/lib/axios.config";
import z from "zod";

const ShippingAddress = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [addresses, setAddresses] = useState<AddressType[]>([]);

  // Fetch addresses when component mounts
  useEffect(() => {
    const fetchAddresses = async () => {
      const data = await GetShippingAddresses();
      if (data) setAddresses(data);
    };
    fetchAddresses();
  }, []);

  const handleAddShippingAddress = async (data: AddShippingAddressInput) => {
    const newAddress = await AddShippingAddress(data);
    if (newAddress) {
      setAddresses((prevAddresses) => [...prevAddresses, newAddress]);
      setIsModalOpen(false);
    } else {
      console.error("Error adding shipping address");
      setIsModalOpen(false);
    }
  };
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Shipping Addresses</CardTitle>
        <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
          <DialogTrigger asChild>
            <Button>Add New Address</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New Shipping Address</DialogTitle>
              <DialogDescription>
                Fill in the form below to add a new shipping address.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Address Nickname</Label>
                <Input id="name" placeholder="e.g. Home, Work" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="address">Address</Label>
                <Input id="address" placeholder="123 Main St, Anytown, USA" />
              </div>
              <Button
                onClick={() => {
                  handleAddShippingAddress({
                    first_name: "AAmaechi",
                    last_name: "Doe",
                    phone: "08012345678",
                    address: "Ice hub",
                    country: "Nigeria",
                    state: "Lagos",
                    lga: "Ikeja",
                    zip_code: "100001",
                  });
                }}
              >
                Save Address
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {addresses.map((address) => (
            <div key={address.id} className="p-4 border rounded-md">
              <p className="font-semibold">{address.country}</p>
              <p>{address.address}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default ShippingAddress;

async function GetShippingAddresses(): Promise<AddressType[] | null> {
  try {
    const response = await axiosInstance.get("api/address");
    return response.data as AddressType[];
  } catch (error) {
    console.error("Error fetching shipping addresses:", error);
    return null;
  }
}

async function AddShippingAddress(
  data: AddShippingAddressInput
): Promise<AddressType | null> {
  try {
    const response = await axiosInstance.post("api/address", data);
    return response.data as AddressType;
  } catch (error) {
    console.error("Error adding shipping address:", error);
    return null;
  }
}

const addShippingAddresSchema = z.object({
  first_name: z.string().min(1, "Name is required"),
  last_name: z.string().min(1, "Name is required"),
  phone: z.string().min(11, "Name is required"),
  address: z.string().min(1, "Name is required"),
  country: z.string().min(1, "Name is required"),
  state: z.string().min(1, "Name is required"),
  lga: z.string().min(1, "Name is required"),
  zip_code: z.string().min(1, "Name is required"),
});

type AddShippingAddressInput = z.infer<typeof addShippingAddresSchema>;
