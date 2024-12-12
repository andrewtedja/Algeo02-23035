import Image from "next/image";
import { Layout } from "@/components/layout";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
	Pagination,
	PaginationContent,
	PaginationItem,
	PaginationLink,
	PaginationNext,
	PaginationPrevious,
} from "@/components/ui/pagination";

export default function SearchAlbumPage() {
	return (
		<Layout>
			<h1 className="text-3xl font-bold mb-6">Search by Album Picture</h1>
			<div className="space-y-6">
				<div className="p-6 bg-muted rounded-lg">
					<div className="aspect-video bg-background mb-4 rounded relative">
						<Image
							src="/placeholder.svg"
							alt="Album cover preview"
							layout="fill"
							objectFit="contain"
						/>
					</div>
					<div className="flex gap-2">
						<Button>Search</Button>
						<Button variant="outline">Cancel</Button>
					</div>
				</div>
				<div>
					<h2 className="text-2xl font-semibold mb-2">
						Heres What We Found...
					</h2>
					<p className="text-muted-foreground mb-4">
						Runtime: XXXXX ms
					</p>
				</div>
				<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
					{[...Array(12)].map((_, i) => (
						<Card key={i} className="overflow-hidden">
							<div className="aspect-square relative">
								<Image
									src="/placeholder.svg"
									alt="Album cover"
									layout="fill"
									objectFit="cover"
								/>
							</div>
							<div className="p-4">
								<h3 className="font-semibold">Title</h3>
								<p className="text-sm text-muted-foreground">
									Artist
								</p>
								<Badge variant="secondary" className="mt-2">
									Match: XX.X%
								</Badge>
							</div>
						</Card>
					))}
				</div>
				<Pagination>
					<PaginationContent>
						<PaginationItem>
							<PaginationPrevious href="#" />
						</PaginationItem>
						<PaginationItem>
							<PaginationLink href="#" isActive>
								1
							</PaginationLink>
						</PaginationItem>
						<PaginationItem>
							<PaginationLink href="#">2</PaginationLink>
						</PaginationItem>
						<PaginationItem>
							<PaginationLink href="#">3</PaginationLink>
						</PaginationItem>
						<PaginationItem>
							<PaginationNext href="#" />
						</PaginationItem>
					</PaginationContent>
				</Pagination>
			</div>
		</Layout>
	);
}
