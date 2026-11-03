
const { createApp } = Vue

const headerVue = createApp({
  data: function () {
    return {
    }
  },
}).mount('#header')

const footerVue = createApp({
  data: function () {
    return {
      year: new Date().getFullYear(),
      version: '1.1.3',
      isTop: true
    }
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
      ytms: YTMS,
      products: PRODUCTS,
      updated: UPDATED_AT,
      showEmptyYTM: false,
      resloveYtms: YTMS,
      region: 'all',
      showFilter: true,
      showMap: false,
      showMapYtm: undefined,
    }
  },
  methods: {
    triggerFilterBlock: function () {
      this.showFilter = !this.showFilter
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
      let target = this.products.find((prod) => prod.key === key)
      if (!target) {
        return 'bg-zinc-300 border-zinc-300 text-zinc-800'
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
    getUpdated: function () {
      let date = new Date(this.updated * 1000)
      let pad = (num) => String(num).padStart(2, '0')
      return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日 ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
    },
    updateList: function () {
      switch (this.region) {
        case 'all':
          this.resloveYtms = this.ytms
          break;
        case 'tpe-mrt':
        case 'kh-mrt':
        case 'direct':
          this.resloveYtms = this.ytms.filter(ytm => ytm.region === this.region)
          break;
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
          abbr = ytm.name.split('-')[1]
        case 'direct':
          prefix = '門市'
          abbr = ytm.abbr
      }

      if (ytm.abbr) {
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
  mounted: function () {
    let width = window.innerWidth
    if (width < 768) {
      this.showFilter = false
    }

    this.region = Cookies.get('regionFilter') ? Cookies.get('regionFilter') : 'all'
    this.showEmptyYTM = Cookies.get('showEmptyYTM') === 'true'
    let productFilter = Cookies.get('productFilter')
    if (productFilter) {
      let prod = this.products.find((p) => p.key === productFilter)
      if (prod) {
        prod.enable = true
      }
    }

    this.updateList()
  },
}).mount('#main')
