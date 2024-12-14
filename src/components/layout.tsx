"use client";

import { Home, Music, ImageIcon, Upload } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

import {
	Sidebar,
	SidebarContent,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	SidebarProvider,
} from "@/components/ui/sidebar";

type LayoutProps = {
	children: React.ReactNode;
	title?: string;
};

export function Layout({ children, title = "Home" }: LayoutProps) {
	const pathname = usePathname();

	const menuItems = [
		{ icon: Home, label: "Home", href: "/" },
		{ icon: Music, label: "Search by Audio", href: "/search/audio" },
		{ icon: ImageIcon, label: "Search by Album", href: "/search/album" },
		{ icon: Upload, label: "Upload Mapper", href: "/upload" },
	];

	return (
		<SidebarProvider>
			<div className="flex min-h-screen">
				<Sidebar>
					<SidebarHeader className="p-8 pb-10 bg-[#363740] text-[#A4A6B3]">
						<Link href="/" className="flex items-center gap-2">
							<div className="rounded-lg">
								<Image
									src="/images/logo.png"
									alt="SongSmart Logo"
									width={35}
									height={35}
								/>
							</div>
							<span className="font-semibold text-xl">
								SongSmart
							</span>
						</Link>
					</SidebarHeader>
					<SidebarContent className="bg-[#363740] text-white">
						<SidebarMenu className="p-0 m-0">
							{menuItems.map((item) => {
								const isActive = pathname === item.href;

								return (
									<SidebarMenuItem key={item.label}>
										<SidebarMenuButton
											asChild
											className={`relative p-8 h-10 text-sm rounded-none tracking-widest transition-colors ${
												isActive
													? "bg-[#41434d] text-white before:absolute before:top-0 before:left-0 before:h-full before:w-[3px] before:bg-white"
													: " hover:text-white text-[#A4A6B3]"
											}`}
										>
											<Link
												href={item.href}
												className="flex items-center gap-2"
											>
												<item.icon className="h-4 w-4" />
												<span>{item.label}</span>
											</Link>
										</SidebarMenuButton>
									</SidebarMenuItem>
								);
							})}
						</SidebarMenu>
					</SidebarContent>
				</Sidebar>
			</div>
			<main className="flex-1 p-6 w-full bg-white">
				<div className="flex items-center font-semibold text-md pt-2">
					{title}
				</div>
				{children}
			</main>
		</SidebarProvider>
	);
}
