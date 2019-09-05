import json
from lxml import etree
from io import BytesIO
import boto3
import os


MOVIES_DB = "movies.db"
MOVIES_DB_FILE = "/tmp/{}".format(MOVIES_DB)

def load_movies_db():
	try:
		if not os.path.isfile(MOVIES_DB_FILE) or os.stat(MOVIES_DB_FILE).st_size == 0 :
			with open(".env", "r") as f:
				role = json.loads(f.read())

			session = boto3.Session(
				aws_access_key_id=role["aws_access_key_id"],
				aws_secret_access_key=role["aws_secret_access_key"],
			)
			s3 = session.resource('s3')
			s3.meta.client.download_file(os.environ["movies_db_bucket"], MOVIES_DB, "/tmp/movies.db")

		else:
			pass

		with open(MOVIES_DB_FILE, 'rd') as f:
			xml = f.read()
		db = BytesIO(xml)
		parser = etree.XMLParser()
		doc = etree.parse(db)
		return doc

	except Exception as e:
		print (e)
		return False

	finally:
		f.close()


def lambda_handler(event, context):
	try:
		found = []
		result = {}
		movie_obj =  event["body"]
		parser = etree.XMLParser(encoding=None, attribute_defaults=False, dtd_validation=False, load_dtd=True, no_network=False, recover=False, resolve_entities=True)
		movie = etree.fromstring(movie_obj, parser).text
		movies = load_movies_db()
		if movies:
			root = movies.getroot()
			movie_list = root.getchildren()
			for element in movie_list:
				for mov in element.iter():
					if mov.tag == "name" and movie.lower() in mov.text.lower():
						genre = []
						return_object = {}
						for x in element.iter():
							if x.tag == "name":
								return_object["name"] = x.text
								continue
							if x.tag == "initial_release_date":
								return_object["release_data"] = x.text
								continue
							if x.tag == "directed_by":
								return_object["director"] = x.text
								continue
							if x.tag == "genre":
								genre.append(x.text)
								continue

						return_object["genre"] = ','.join(genre)
						found.append(return_object)
					else:
						continue
		else:
			pass

	except Exception as e:
		print (e)

	if len(found) == 0:
		msg = "Could not find movies with: " + movie
		result["status"] = "err"
		result["result"] = msg
	else:
		result["status"] = "ok"
		result["result"] = found

	return {
		'statusCode': 200,
		'body': json.dumps(result)
	}
