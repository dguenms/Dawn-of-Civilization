import re


DEFINES_FILE_PATH = "Assets/XML/GlobalDefinesVersion.xml"


def update_version():
	with open(DEFINES_FILE_PATH, "r+") as file:
		file_content = file.read()
		version = re.search(r"<DefineTextVal>(.*)</DefineTextVal>", file_content).group(1)
		
		if "-" in version:
			base_version, suffix = version.split("-")
			new_version = f"{base_version}-{int(suffix)+1}"
		else:
			new_version = f"{version}-1"
		
		print(f"Update mod version to {new_version}")
		
		file.seek(0)
		file.write(file_content.replace(version, new_version))
		file.truncate()


if __name__ == "__main__":
	update_version()