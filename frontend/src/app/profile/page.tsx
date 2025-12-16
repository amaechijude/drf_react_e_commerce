
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import UserProfile from "@/components/profile/user-profile";
import Orders from "@/components/profile/orders";
import ShippingAddress from "@/components/profile/shipping-address";
import Cart from "@/components/profile/cart";
import PaymentMethods from "@/components/profile/payment-methods";

const ProfilePage = () => {
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">My Profile</h1>
      <Tabs defaultValue="profile">
        <TabsList>
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="orders">Orders</TabsTrigger>
          <TabsTrigger value="shipping">Shipping Address</TabsTrigger>
          <TabsTrigger value="cart">Cart</TabsTrigger>
          <TabsTrigger value="payment">Payment Methods</TabsTrigger>
        </TabsList>
        <TabsContent value="profile">
          <UserProfile />
        </TabsContent>
        <TabsContent value="orders">
          <Orders />
        </TabsContent>
        <TabsContent value="shipping">
          <ShippingAddress />
        </TabsContent>
        <TabsContent value="cart">
          <Cart />
        </TabsContent>
        <TabsContent value="payment">
          <PaymentMethods />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProfilePage;
