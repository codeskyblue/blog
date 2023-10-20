#!/bin/bash -ex
#

export PATH=/usr/bin:/usr/local/bin:/home/codeskyblue/.nvm/versions/node/v16.20.0/bin

dotenv -e .env npm run sync
npm run publish
