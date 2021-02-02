DEST=static_server:/home/static/
build:
	docker-compose build
up:
	docker-compose up -d
shell:
	docker-compose exec server bash
compile:
	mkdir -p dist/node_modules/
	cp -fr node_modules/jsdom dist/node_modules/
	cp -fr node_modules/canvas dist/node_modules/
	(cd dist && tar -zcvf node_modules.tgz node_modules)
	yarn run build-linux
	scp dist/node_modules.tgz ${DEST}
	scp dist/tt-signer ${DEST}
	scp install.sh ${DEST}
	# (cd dist && rsync -avzu --progress . root@192.168.4.203:/home/osint/tt-signer/)