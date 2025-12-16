"use client";
import Link from "next/link";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import { Button } from "../ui/button";
import { useAuth } from "@/hook/use-auth";

export function NavBar() {
  const { user, isLoggedIn, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
        <a href="#" className="text-2xl font-bold text-blue-600">
          ShopSphere
        </a>
        <div className="hidden md:flex space-x-6 items-center">
          <a href="#" className="text-gray-600 hover:text-blue-500">
            Home
          </a>
          <a href="product" className="text-gray-600 hover:text-blue-500">
            Shop
          </a>
          <a href="#" className="text-gray-600 hover:text-blue-500">
            About
          </a>
          <a href="#" className="text-gray-600 hover:text-blue-500">
            Contact
          </a>
          {isLoggedIn ? (
            <div>
              <span className="text-gray-800">Hello, {user?.email}</span>
              <Link
                href="/profile"
                className="ml-4 text-blue-600 hover:underline"
              >
                Profile
              </Link>
              <Button onClick={logout}>Logout</Button>
            </div>
          ) : (
            <div>
              <Link
                href={"/auth/register"}
                className="text-gray-600 hover:text-blue-500"
              >
                Register
              </Link>
              <Link
                href={"/auth/login"}
                className="text-gray-600 hover:text-blue-500"
              >
                Login
              </Link>
            </div>
          )}
        </div>
        <div className="flex items-center space-x-4">
          <Button className="text-gray-600 hover:text-blue-500">
            <svg
              className="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              ></path>
            </svg>
          </Button>
          <Button className="text-gray-600 hover:text-blue-500">
            <svg
              className="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
              ></path>
            </svg>
          </Button>
          <button
            className="md:hidden text-gray-600 hover:text-blue-500 focus:outline-none ml-4"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </nav>
      {isMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 px-6 py-4 space-y-4">
          <a href="#" className="block text-gray-600 hover:text-blue-500">
            Home
          </a>
          <a href="product" className="block text-gray-600 hover:text-blue-500">
            Shop
          </a>
          <a href="#" className="block text-gray-600 hover:text-blue-500">
            About
          </a>
          <a href="#" className="block text-gray-600 hover:text-blue-500">
            Contact
          </a>
          {isLoggedIn ? (
            <div className="pt-4 border-t border-gray-100">
              <div className="flex items-center mb-4">
                {user?.avatar && (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={user.avatar}
                    alt="Avatar"
                    className="h-8 w-8 rounded-full mr-2"
                  />
                )}
                <span className="text-gray-800">{user?.email}</span>
              </div>
              <Link
                href="/profile"
                className="block text-blue-600 hover:underline mb-2"
              >
                Profile
              </Link>
              <Button onClick={logout} className="w-full">
                Logout
              </Button>
            </div>
          ) : (
            <div className="flex flex-col space-y-2 pt-4 border-t border-gray-100">
              <Link
                href={"/auth/register"}
                className="block text-gray-600 hover:text-blue-500"
              >
                Register
              </Link>
              <Link
                href={"/auth/login"}
                className="block text-gray-600 hover:text-blue-500"
              >
                Login
              </Link>
            </div>
          )}
        </div>
      )}
    </header>
  );
}
