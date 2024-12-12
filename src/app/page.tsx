import { Layout } from "@/components/layout";

export default function HomePage() {
	return (
		<Layout>
			<h1 className="text-3xl font-bold">Welcome to SongSmart</h1>
			<p className="mt-4 text-lg text-muted-foreground">
				Use the sidebar to navigate to different features of the
				application.
			</p>
		</Layout>
	);
}
