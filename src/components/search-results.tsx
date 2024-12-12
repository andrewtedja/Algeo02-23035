import Image from "next/image";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import {
	Pagination,
	PaginationContent,
	PaginationEllipsis,
	PaginationItem,
	PaginationLink,
	PaginationNext,
	PaginationPrevious,
} from "@/components/ui/pagination";

interface SearchResult {
	title: string;
	artist: string;
	matchPercentage?: number;
	imageUrl: string;
}

interface SearchResultsProps {
	results: SearchResult[];
	isLoading?: boolean;
	runtime?: number;
}

export function SearchResults({
	results,
	isLoading,
	runtime,
}: SearchResultsProps) {
	return (
		<div className="space-y-6">
			{runtime && (
				<div className="text-center">
					<h1 className="text-3xl font-bold">
						Here What We Found...
					</h1>
					<p className="text-muted-foreground">
						Runtime: {runtime} ms
					</p>
				</div>
			)}

			<div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
				{isLoading
					? Array(9)
							.fill(0)
							.map((_, i) => (
								<Card key={i} className="p-4">
									<Skeleton className="h-40 w-full" />
									<div className="mt-4 space-y-2">
										<Skeleton className="h-4 w-2/3" />
										<Skeleton className="h-4 w-1/2" />
									</div>
								</Card>
							))
					: results.map((result, i) => (
							<Card key={i} className="overflow-hidden">
								<div className="aspect-square relative">
									<Image
										src={
											result.imageUrl ||
											"/placeholder.svg"
										}
										alt={`${result.title} by ${result.artist}`}
										layout="fill"
										objectFit="cover"
									/>
								</div>
								<div className="p-4">
									<h3 className="font-semibold">
										{result.title}
									</h3>
									<p className="text-sm text-muted-foreground">
										{result.artist}
									</p>
									{result.matchPercentage && (
										<Badge
											variant="secondary"
											className="mt-2"
										>
											Match: {result.matchPercentage}%
										</Badge>
									)}
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
						<PaginationEllipsis />
					</PaginationItem>
					<PaginationItem>
						<PaginationNext href="#" />
					</PaginationItem>
				</PaginationContent>
			</Pagination>
		</div>
	);
}
