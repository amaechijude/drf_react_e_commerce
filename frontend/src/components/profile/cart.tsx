import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { getUserCart } from "@/lib/data";


const CartComponent = async () => {
  const cart = await getUserCart();
  if (cart === undefined){
    return <div>Empty cart</div>
  }

    const totalPrice = cart.cart_items.reduce((acc, item) => acc + item.product.current_price * item.quantity, 0);
  return (
    <Card>
      <CardHeader>
        <CardTitle>My Cart</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Product</TableHead>
              <TableHead>Price</TableHead>
              <TableHead>Quantity</TableHead>
              <TableHead>Total</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {cart.cart_items.map((item) => (
              <TableRow key={item.id}>
                <TableCell>{item.product.name}</TableCell>
                <TableCell>${item.product.current_price.toFixed(2)}</TableCell>
                <TableCell>{item.quantity}</TableCell>
                <TableCell>${(item.product.current_price * item.quantity).toFixed(2)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <div className="mt-4 text-right">
            <p className="text-lg font-semibold">Total: ${totalPrice.toFixed(2)}</p>
            <Button className="mt-2">Checkout</Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default CartComponent;

