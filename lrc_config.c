#define SUBSTRIPES 3
#define SUBSTRIPE_DATA 2
#define E_BLOCKS 1
#define GLOBAL_S 1

const unsigned char lrc_scheme[(SUBSTRIPE_DATA + 1) * SUBSTRIPES + E_BLOCKS + GLOBAL_S] =
{0x0, 0x0, 0xc0, 0x1, 0x1, 0xc1, 0x2, 0x2, 0xc2, 0xee, 0xff};

// it is just lrc_scheme without 0xee, 0xff and 0xcN
const unsigned char lrc_data[SUBSTRIPE_DATA * SUBSTRIPES] =
{0x0, 0x0, 0x1, 0x1, 0x2, 0x2};

// it is place of global syndrome
const int lrc_gs[1] =
{10};

// places of all local syndromes
const int lrc_ls[SUBSTRIPES] = {2,5,8};
// empty place
const int lrc_eb =9;
// not-data blocks, ordered by increasing
const int lrc_offset[SUBSTRIPES + E_BLOCKS + GLOBAL_S] = {2,5,8,9,10};
// number of the last data block
const int lrc_ldb =7;

