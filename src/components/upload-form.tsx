import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Upload } from "lucide-react";
import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface UploadFormProps {
	title: string;
	buttonText: string;
	onUpload: (file: File) => void;
}

export function UploadForm({ title, buttonText, onUpload }: UploadFormProps) {
	const [showCancelAlert, setShowCancelAlert] = useState(false);
	const [selectedFile, setSelectedFile] = useState<File | null>(null);

	const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0];
		if (file) {
			setSelectedFile(file);
		}
	};

	const handleUpload = () => {
		if (selectedFile) {
			onUpload(selectedFile);
		}
	};

	return (
		<div className="space-y-6">
			<h1 className="text-2xl font-bold">{title}</h1>

			<div className="grid place-items-center gap-6 p-8">
				<div className="w-full max-w-xl aspect-[4/3] rounded-lg border-2 border-dashed border-muted-foreground/25 hover:border-muted-foreground/50 transition-colors">
					<label
						htmlFor="file-upload"
						className="relative flex h-full w-full cursor-pointer flex-col items-center justify-center gap-2"
					>
						<div className="rounded-full bg-muted p-4">
							<Upload className="h-6 w-6 text-muted-foreground" />
						</div>
						<p className="text-lg font-medium">Drag files</p>
						<p className="text-sm text-muted-foreground">
							Click to upload files (files should be under 10 MB)
						</p>
						<Input
							id="file-upload"
							type="file"
							className="sr-only"
							onChange={handleFileChange}
							accept="audio/*,image/*"
						/>
					</label>
				</div>

				<div className="flex gap-2">
					<Button
						size="lg"
						onClick={handleUpload}
						disabled={!selectedFile}
					>
						{buttonText}
					</Button>
					<Button
						size="lg"
						variant="outline"
						onClick={() => setShowCancelAlert(true)}
					>
						Cancel
					</Button>
				</div>
			</div>

			<AlertDialog
				open={showCancelAlert}
				onOpenChange={setShowCancelAlert}
			>
				<AlertDialogContent>
					<AlertDialogHeader>
						<AlertDialogTitle>
							Are you sure you want to cancel?
						</AlertDialogTitle>
						<AlertDialogDescription>
							This will clear your current upload progress.
						</AlertDialogDescription>
					</AlertDialogHeader>
					<AlertDialogFooter>
						<AlertDialogCancel>Back</AlertDialogCancel>
						<AlertDialogAction
							onClick={() => {
								setSelectedFile(null);
								setShowCancelAlert(false);
							}}
						>
							Yes, cancel
						</AlertDialogAction>
					</AlertDialogFooter>
				</AlertDialogContent>
			</AlertDialog>
		</div>
	);
}
