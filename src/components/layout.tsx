import { Home, Music, ImageIcon, Upload } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import {
	Sidebar,
	SidebarContent,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	SidebarProvider,
} from "@/components/ui/sidebar";

export function Layout({ children }: { children: React.ReactNode }) {
	const menuItems = [
		{ icon: Home, label: "Home", href: "/" },
		{ icon: Music, label: "Search by Audio", href: "/search/audio" },
		{ icon: ImageIcon, label: "Search by Album", href: "/search/album" },
		{ icon: Upload, label: "Upload Mapper", href: "/upload" },
	];

	return (
		<SidebarProvider>
			<div className="flex min-h-screen ">
				<Sidebar>
					<SidebarHeader className="p-4 bg-[#363740] text-[#A4A6B3]">
						<Link href="/" className="flex items-center gap-2">
							<div className="rounded-lg">
								<Image
									src="/images/logo.png"
									alt="SongSmart Logo"
									width={30}
									height={30}
								/>
							</div>
							<span className="font-semibold">SongSmart</span>
						</Link>
					</SidebarHeader>
					<SidebarContent className="bg-[#363740] text-white">
						<SidebarMenu>
							{menuItems.map((item) => (
								<SidebarMenuItem key={item.label}>
									<SidebarMenuButton
										asChild
										className="h-10 hover:bg-[#50525e] hover:text-white"
									>
										<Link
											href={item.href}
											className="flex items-center gap-2 text-[#A4A6B3] rounded-none transition-colors"
										>
											<item.icon className="h-4 w-4" />
											<span>{item.label}</span>
										</Link>
									</SidebarMenuButton>
								</SidebarMenuItem>
							))}
						</SidebarMenu>
					</SidebarContent>
				</Sidebar>
				<main className="flex-1 p-6">{children}</main>
			</div>
		</SidebarProvider>
	);
}
