// THPS2's side of the extended draw distance. The engine is shared with THPS3 and lives in the Host (src/draw_distance_thps23.cpp, with
// the notes); this file holds what is THPS2's own: the profile (offsets and sizes of the renderer's lists, no THPS3 extras) and the zone
// ownership profile.
#include "draw_distance_thps23.h"
#include "zone_ownership.h"

// The renderer's mesh queue: 512 entries (+0x1CC, count +0x21CC) and the depth-sorted list of translucent meshes: 96 entries (+0x21D8,
// count +0x2AD8); the batch flag is +0x2AE0. The vertex pools stay the game's own, and there is no list of put-aside items.
const thps::dd23::Profile& thps::dd23::profile() {
    static const Profile p{0x21CC, 512, 0x2AD8, 96, 0x2AE0, false, nullptr, nullptr};
    return p;
}

// Zone ownership (src/zone_ownership.h): the box command shows on 1.
const thps::zones::Profile& thps::zones::profile() {
    static const Profile p{false, 0x40, 0x34};
    return p;
}
