import { Layout } from "@/components/layout";
import { Check } from "lucide-react";

export default function UploadSuccessPage() {
	return (
		<Layout title="Upload">
			<div className="min-h-[90vh] flex flex-col items-center justify-center">
				<div className="bg-green-500 text-white rounded-full mb-5 p-4 animate-bounce">
					<Check size={48} />
				</div>
				<div>
					<h1 className="text-3xl font-bold text-center">
						Mapper Uploaded Succesfully!
					</h1>
				</div>
			</div>
		</Layout>
	);
}
