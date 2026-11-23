// Writes sidestore.json (AltStore/SideStore source format) next to Dusk.ipa in CI.
// The version must match the built app (MARKETING_VERSION = <major>.<minor>.<run number>) so
// SideStore can tell when an update is available.
const fs = require('fs');

const { RUN, REPO, SHA } = process.env;
const base = require('../package.json').version.split('.').slice(0, 2).join('.');
const version = `${base}.${RUN}`;
const ipa = `https://github.com/${REPO}/releases/download/ios-latest/Dusk.ipa`;
const icon = `https://raw.githubusercontent.com/${REPO}/${SHA}/assets/icon-ios.png`;
const now = new Date().toISOString();
const size = fs.statSync('Dusk.ipa').size;

const app = {
  name: 'Dusk Music',
  bundleIdentifier: 'io.github.zxypablo11.dusk',
  developerName: 'zxypablo11',
  subtitle: 'Free music player',
  iconURL: icon,
  tintColor: '7C4DFF',
  localizedDescription: 'Dusk Music — free, ad-free music player by zxypablo11. Stream from YouTube, YouTube Music and SoundCloud, synced lyrics, offline songs, playlists and recommendations. Independent open source (MIT). Not affiliated with YouTube, SoundCloud, Spotify, Riff or Muriel.',
  screenshotURLs: ['home', 'player', 'search'].map((n) => `https://raw.githubusercontent.com/${REPO}/${SHA}/site/shots/${n}.jpg`),
  versions: [{ version, buildVersion: String(RUN), date: now, size, downloadURL: ipa, minOSVersion: '15.0' }],
  version, versionDate: now, size, downloadURL: ipa,
  appPermissions: {},
};

fs.writeFileSync('sidestore.json', JSON.stringify({
  name: 'Dusk Music',
  identifier: 'io.github.zxypablo11.dusk.source',
  iconURL: icon,
  website: `https://${REPO.split('/')[0]}.github.io/${REPO.split('/')[1]}/`,
  tintColor: '7C4DFF',
  apps: [app],
  news: [],
}, null, 2));
console.log(`sidestore.json: Dusk ${version}, ${size} bytes`);
