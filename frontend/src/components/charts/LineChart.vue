<script>
import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Line,
  mixins: [reactiveProp],
  props: {
    chartData: {
      type: Object,
      required: true
    },
    options: {
      type: Object,
      default: () => ({
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: 'rgba(0,0,0,0.8)',
          titleFontColor: '#ffffff',
          bodyFontColor: '#ffffff',
          bodySpacing: 4,
          xPadding: 12,
          mode: 'nearest',
          intersect: 0,
          position: 'nearest'
        },
        scales: {
          yAxes: [{
            gridLines: {
              drawBorder: false,
              color: 'rgba(225,78,202,0.1)',
              zeroLineColor: 'transparent'
            },
            ticks: {
              padding: 20,
              fontColor: '#9e9e9e'
            }
          }],
          xAxes: [{
            gridLines: {
              drawBorder: false,
              color: 'rgba(225,78,202,0.1)',
              zeroLineColor: 'transparent'
            },
            ticks: {
              padding: 20,
              fontColor: '#9e9e9e'
            }
          }]
        }
      })
    }
  },
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
}
</script> 