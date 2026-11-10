
const { createApp } = Vue

const headerVue = createApp({
  data: function () {
    return {
    }
  },
  methods: {
    smooth2Top: function () {
      window.scrollTo({top: 0, behavior: 'smooth'})
    },
  },
}).mount('#header')

const footerVue = createApp({
  data: function () {
    return {
      year: new Date().getFullYear(),
      version: '1.3.1',
      isTop: true
    }
  },
  methods: {
    smooth2Top: function () {
      window.scrollTo({top: 0, behavior: 'smooth'})
    },
  },
  mounted: function () {
    this.isTop = window.scrollY <= 0
    window.addEventListener('scroll', () => {
      this.isTop = window.scrollY <= 0
    })
  },
}).mount('#footer')

const mainVue = createApp({
  data: function () {
    return {
      timer: {},
      now: Date.now(),
      ytms: {},
      products: {},
      updated: 0,
      showEmptyYTM: false,
      resloveYtms: {},
      region: 'all',
      showFilter: true,
      showFilterMobile: false,
      showMap: false,
      showMapYtm: undefined,
      inDetailRegion: false,
      regionList: [
        {
          group: undefined,
          regions: [
            { name: '所有 YTM', value: 'all' },
          ],
        },
        {
          group: '台北捷運',
          regions: [
            { name: '台北捷運-全線', value: 'tpe-mrt', icon: 'tpe-mrt/brand.svg' },
            { name: '台北捷運-板南線', value: 'tpe-mrt/bannan', icon: 'tpe-mrt/bl.svg' },
            { name: '台北捷運-文湖線', value: 'tpe-mrt/wenhu', icon: 'tpe-mrt/br.svg' },
            { name: '台北捷運-淡水信義線', value: 'tpe-mrt/tamsui-xinyi', icon: 'tpe-mrt/r.svg' },
            { name: '台北捷運-中和新蘆線', value: 'tpe-mrt/zhonghe-xinlu', icon: 'tpe-mrt/o.svg' },
            { name: '台北捷運-松山新店線', value: 'tpe-mrt/songshan-xindian', icon: 'tpe-mrt/g.svg' },
            { name: '台北捷運-環狀線', value: 'tpe-mrt/circular', icon: 'tpe-mrt/y.svg' },
          ],
        },
        {
          group: '高雄捷運',
          regions: [
            { name: '高雄捷運-全線', value: 'kh-mrt', icon: 'kh-mrt/brand.svg' },
            { name: '高雄捷運-紅線', value: 'kh-mrt/red', icon: 'kh-mrt/r.svg' },
          ],
        },
        {
          group: '門市',
          regions: [
            { name: '全台門市', value: 'direct', icon: 'yannick.svg' },
            { name: '北區門市', value: 'direct/northern', icon: 'yannick.svg' },
            { name: '中區門市', value: 'direct/central', icon: 'yannick.svg' },
            { name: '南區門市', value: 'direct/southern', icon: 'yannick.svg' },
          ],
        },
      ]
    }
  },
  methods: {
    fetchYtmData: function () {
      axios.get(`/assets/data/ytm-stock.json?v=${this.now}`)
      .then((resp) => {
        this.ytms = resp.data.ytms
        this.updated = resp.data.updated
        this.products = resp.data.products

        this.fetchCookiesFilter()
        this.updateList()
      })
      .catch((error) => {
        console.error(error)
      })
    },
    fetchCookiesFilter: function () {
      this.region = Cookies.get('regionFilter') ? Cookies.get('regionFilter') : 'all'
      this.showEmptyYTM = Cookies.get('showEmptyYTM') === 'true'
      let productFilter = Cookies.get('productFilter')
      if (productFilter) {
        let prod = this.products.find((p) => p.key === productFilter)
        if (prod) {
          prod.enable = true
        }
      }
    },
    triggerFilterBlock: function () {
      this.showFilter = !this.showFilter
      this.showFilterMobile = this.showFilter
    },
    triggerProductFilter: function (key) {
      this.products.forEach((prod) => {
        if (prod.key !== key) {
          prod.enable = false
        }
      })

      let target = this.products.find((prod) => prod.key === key)
      target.enable = !target.enable
      this.updateList()

      if (target.enable) {
        Cookies.set('productFilter', key)
      } else {
        Cookies.remove('productFilter')
      }
    },
    resetRegionFilter: function () {
      this.region = 'all'
      this.updateList()
      Cookies.remove('regionFilter')
    },
    resetProductFilter: function () {
      this.products.forEach((prod) => {
        prod.enable = false
      })

      this.updateList()
      Cookies.remove('productFilter')
    },
    resetFilters: function () {
      this.region = 'all'
      this.showEmptyYTM = false
      this.products.forEach((prod) => {
        prod.enable = false
      })

      this.updateList()

      Cookies.remove('regionFilter')
      Cookies.remove('showEmptyYTM')
      Cookies.remove('productFilter')
    },
    getProductStyle: function (key) {
      if (!this.isFilterProduct(key)) {
        return 'bg-zinc-300 dark:bg-zinc-800 border-zinc-300 dark:border-zinc-800 text-zinc-500'
      }

      let target = this.products.find((prod) => prod.key === key)
      if (!target) {
        return 'bgbg-zinc-300 border-zinc-300 text-zinc-800'
      }
      return target.style
    },
    getProductName: function (key) {
      let target = this.products.find((prod) => prod.key === key)
      return target.name
    },
    getMrtIcon: function (name) {
      mrt = ''
      if (name.split('-').length > 1) {
        mrt = name.split('-')[0]
      }

      switch (mrt) {
        case '環狀線':
          return '/assets/icons/tpe-mrt/y.svg'
        case '松山新店線':
          return '/assets/icons/tpe-mrt/g.svg'
        case '中和新蘆線':
          return '/assets/icons/tpe-mrt/o.svg'
        case '文湖線':
          return '/assets/icons/tpe-mrt/br.svg'
        case '板南線':
          return '/assets/icons/tpe-mrt/bl.svg'
        case '淡水信義線':
          return '/assets/icons/tpe-mrt/r.svg'
        case '紅線':
          return '/assets/icons/kh-mrt/r.svg'
      }

      return ''
    },
    isFilterProduct: function (product) {
      let productFilter = this.products.find((prod) => prod.enable)
      if (productFilter) {
        return productFilter.key === product
      } else {
        return true
      }
    },
    updateList: function () {
      this.inDetailRegion = false

      switch (this.region) {
        case 'all':
          this.resloveYtms = this.ytms
          break;
        case 'direct':
          this.inDetailRegion = true
        case 'tpe-mrt':
        case 'kh-mrt':
          this.resloveYtms = this.ytms.filter(ytm => ytm.region === this.region)
          break;
        default:
          mainRegion = this.region.split('/')[0]
          subRegion = this.region.split('/')[1]
          if (!subRegion) {
            this.resloveYtms = this.ytms
            break;
          }

          this.inDetailRegion = true
          this.resloveYtms = this.ytms.filter(ytm => ytm.region === mainRegion && ytm.subRegion === subRegion)
      }

      if (!this.showEmptyYTM) {
        this.resloveYtms = this.resloveYtms.filter(ytm => ytm.stocks.length > 0)
      }

      let productFilter = this.products.find((prod) => prod.enable)
      if (productFilter) {
        this.resloveYtms = this.resloveYtms.filter(ytm => ytm.stocks.some(stock => stock.key === productFilter.key))
      }
    },
    showMapModal: function (ytm) {
      this.showMapYtm = ytm
      this.showMap = true
      document.body.classList.add('overflow-hidden')
    },
    closeMapModal: function () {
      document.body.classList.remove('overflow-hidden')
      this.showMap = false
    },
    getYtmMap: function (ytm) {
      if (!ytm) {
        return ''
      }

      abbr = ''
      prefix = ''
      switch (ytm.region) {
        case 'tpe-mrt':
        case 'kh-mrt':
          prefix = '1-捷運路線圖'
          abbr = ytm.abbr ?? ytm.name.split('-')[1]
          break;
        case 'direct':
          prefix = '門市'
          abbr = ytm.abbr
          break;
      }

      if (abbr) {
        switch (ytm.ytm_gen) {
          case 1:
            return encodeURI(`https://photo.yannick.com.tw/0.YTM查詢-${prefix}-${abbr}.jpg`)
          case 2:
            return encodeURI(`https://photo.yannick.com.tw/photo/YTM2/0.YTM查詢-${prefix}-${abbr}.jpg`)
          case 3:
            return encodeURI(`https://photo.yannick.com.tw/photo/YTM2/0.YTM查詢-${prefix}-${abbr}-01.jpg`)
          case 4:
            return encodeURI(`https://photo.yannick.com.tw/photo/YTM2/0.YTM查詢-${prefix}-2${abbr}-01.jpg`)
          case 5:
            return encodeURI(`https://photo.yannick.com.tw/photo/0.YTM查詢-${prefix}-${abbr}.jpg`)
          default:
          case 6:
            return encodeURI(`https://photo.yannick.com.tw/photo/YTM2/0.YTM查詢-${prefix}-${abbr}- 中文-01.jpg`)
        }
      } else {
        switch (ytm.ytm_gen) {
          default:
          case 1:
            return encodeURI(`https://photo.yannick.com.tw/0.YTM查詢-${prefix}.jpg`)
        }
      }
    },
  },
  watch: {
    region: function (newVal) {
      this.updateList()
      Cookies.set('regionFilter', newVal)
    },
    showEmptyYTM: function (newVal) {
      this.updateList()
      Cookies.set('showEmptyYTM', newVal)
    }
  },
  computed: {
    filterRegion: function () {
      return this.regionList
        .flatMap(group => group.regions)
        .find(r => r.value === this.region)?.name || ''
    },
    filterRegionIcon: function () {
      return this.regionList
        .flatMap(group => group.regions)
        .find(r => r.value === this.region)?.icon || ''
    },
    groupedRegions: function () {
      return this.regionList.filter(item => item.group)
    },
    filterProduct: function () {
      let productFilter = this.products.find((prod) => prod.enable)
      if (productFilter) {
        return productFilter.name
      }
      return ''
    },
    getUpdated: function () {
      let date = new Date(this.updated * 1000)
      let pad = (num) => String(num).padStart(2, '0')
      let diff = Math.round((this.now - date) / 1000)
      let diffStr = diff >= 60 ? `${Math.round(diff / 60)} 分鐘前` : `${diff} 秒前`
      return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())} (${diffStr})`
    },
  },
  beforeMount: function () {
    this.fetchYtmData()

    let width = window.innerWidth

    if (width < 768) {
      this.showFilter = false
    }
  },
  mounted: function () {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' || e.key === 'Esc') {
        this.closeMapModal()
      }
    })

    this.timer.updateNowTmr = setInterval(() => {
      this.now = Date.now()
    }, 200)

    this.timer.updateDataTmr = setInterval(() => {
      this.fetchYtmData()
    }, 1000 * 30) // 30 sec
  },
}).mount('#main')
